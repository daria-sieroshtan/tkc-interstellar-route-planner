resource "google_project_service" "compute" {
  service            = "compute.googleapis.com"
  disable_on_destroy = false
}

resource "google_service_account" "vm" {
  account_id   = "interstellar-vm-${var.environment}"
  display_name = "Interstellar Route Planner VM (${var.environment})"
}

resource "google_compute_address" "static_ip" {
  name = "interstellar-ip-${var.environment}"

  depends_on = [google_project_service.compute]
}

resource "google_compute_instance" "app" {
  name         = "interstellar-${var.environment}"
  machine_type = var.machine_type

  tags = ["interstellar-${var.environment}"]

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2404-lts-amd64"
      size  = 20
      type  = "pd-ssd"
    }
  }

  network_interface {
    network = "default"
    access_config {
      nat_ip = google_compute_address.static_ip.address
    }
  }

  service_account {
    email  = google_service_account.vm.email
    scopes = ["cloud-platform"]
  }

  metadata = {
    app-repo-url = var.app_repo_url
    db-password  = var.db_password
    environment  = var.environment
  }

  metadata_startup_script = file("${path.module}/startup.sh")

  depends_on = [google_project_service.compute]
}

resource "google_compute_firewall" "allow_http" {
  name    = "interstellar-allow-http-${var.environment}"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["8000"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["interstellar-${var.environment}"]
}

resource "google_compute_firewall" "allow_iap_ssh" {
  name    = "interstellar-allow-iap-ssh-${var.environment}"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["35.235.240.0/20"]
  target_tags   = ["interstellar-${var.environment}"]
}
