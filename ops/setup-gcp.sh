#!/usr/bin/env bash
#
# One-off GCP setup for Interstellar Route Planner.
# Run this once from your local machine with gcloud already authenticated.
#
# Usage:
#   export GCP_PROJECT_ID="your-project-id"
#   export DB_PASSWORD="your-db-password"
#   bash ops/setup-gcp.sh
#
set -euo pipefail

# ── Configuration ───────────────────────────────────────────────────
GCP_PROJECT_ID="${GCP_PROJECT_ID:?Set GCP_PROJECT_ID before running}"
DB_PASSWORD="${DB_PASSWORD:?Set DB_PASSWORD before running}"
GCP_REGION="europe-west2"
GCP_ZONE="europe-west2-a"
GITHUB_REPO="daria-sieroshtan/tkc-interstellar-route-planner"
STATE_BUCKET="interstellar-route-planner-tfstate"
WIF_POOL="github-pool"
WIF_PROVIDER="github-provider"
SA_DEPLOY="github-deploy"

echo "==> Setting project to ${GCP_PROJECT_ID}"
gcloud config set project "${GCP_PROJECT_ID}"

# ── 1. Enable required APIs ────────────────────────────────────────
echo "==> Enabling APIs..."
gcloud services enable \
  compute.googleapis.com \
  iam.googleapis.com \
  iap.googleapis.com \
  cloudresourcemanager.googleapis.com \
  sts.googleapis.com

# ── 2. Create GCS bucket for Terraform state ───────────────────────
echo "==> Creating Terraform state bucket..."
if ! gcloud storage buckets describe "gs://${STATE_BUCKET}" &>/dev/null; then
  gcloud storage buckets create "gs://${STATE_BUCKET}" \
    --location="${GCP_REGION}" \
    --uniform-bucket-level-access
  gcloud storage buckets update "gs://${STATE_BUCKET}" --versioning
else
  echo "    Bucket already exists, skipping."
fi

# ── 3. Create deploy service account ───────────────────────────────
echo "==> Creating deploy service account..."
SA_EMAIL="${SA_DEPLOY}@${GCP_PROJECT_ID}.iam.gserviceaccount.com"

if ! gcloud iam service-accounts describe "${SA_EMAIL}" &>/dev/null; then
  gcloud iam service-accounts create "${SA_DEPLOY}" \
    --display-name="GitHub Actions Deploy"
fi

echo "==> Granting roles to deploy service account..."
for ROLE in \
  roles/compute.instanceAdmin.v1 \
  roles/iap.tunnelResourceAccessor \
  roles/iam.serviceAccountUser \
  roles/storage.admin; do
  gcloud projects add-iam-policy-binding "${GCP_PROJECT_ID}" \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="${ROLE}" \
    --condition=None \
    --quiet
done

# ── 4. Workload Identity Federation ────────────────────────────────
echo "==> Setting up Workload Identity Federation..."
PROJECT_NUMBER=$(gcloud projects describe "${GCP_PROJECT_ID}" --format="value(projectNumber)")

# Create pool
if ! gcloud iam workload-identity-pools describe "${WIF_POOL}" \
  --location="global" &>/dev/null; then
  gcloud iam workload-identity-pools create "${WIF_POOL}" \
    --location="global" \
    --display-name="GitHub Actions Pool"
fi

# Create provider
if ! gcloud iam workload-identity-pools providers describe "${WIF_PROVIDER}" \
  --workload-identity-pool="${WIF_POOL}" \
  --location="global" &>/dev/null; then
  gcloud iam workload-identity-pools providers create-oidc "${WIF_PROVIDER}" \
    --workload-identity-pool="${WIF_POOL}" \
    --location="global" \
    --issuer-uri="https://token.actions.githubusercontent.com" \
    --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
    --attribute-condition="assertion.repository=='${GITHUB_REPO}'"
fi

# Allow GitHub repo to impersonate the deploy SA
gcloud iam service-accounts add-iam-policy-binding "${SA_EMAIL}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${WIF_POOL}/attribute.repository/${GITHUB_REPO}" \
  --quiet

WIF_PROVIDER_FULL="projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${WIF_POOL}/providers/${WIF_PROVIDER}"

# ── 5. Terraform init & apply ──────────────────────────────────────
echo "==> Writing ops/terraform/terraform.tfvars..."
cat > ops/terraform/terraform.tfvars <<EOF
gcp_project  = "${GCP_PROJECT_ID}"
gcp_region   = "${GCP_REGION}"
gcp_zone     = "${GCP_ZONE}"
machine_type = "e2-small"
app_repo_url = "https://github.com/${GITHUB_REPO}.git"
db_password  = "${DB_PASSWORD}"
environment  = "prod"
EOF

echo "==> Running terraform init..."
cd ops/terraform
terraform init

echo "==> Running terraform apply..."
terraform apply

VM_IP=$(terraform output -raw vm_external_ip)
cd ../..

# ── 6. Print GitHub secrets to configure ───────────────────────────
echo ""
echo "============================================================"
echo "  SETUP COMPLETE"
echo "============================================================"
echo ""
echo "VM external IP: ${VM_IP}"
echo "API will be available at: http://${VM_IP}:8000"
echo ""
echo "Add these GitHub repo secrets (Settings > Secrets > Actions):"
echo ""
echo "  GCP_WORKLOAD_IDENTITY_PROVIDER = ${WIF_PROVIDER_FULL}"
echo "  GCP_SERVICE_ACCOUNT            = ${SA_EMAIL}"
echo "  GCP_PROJECT_ID                 = ${GCP_PROJECT_ID}"
echo "  GCP_ZONE                       = ${GCP_ZONE}"
echo ""
echo "Then push to main to trigger a deploy."
