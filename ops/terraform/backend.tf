terraform {
  backend "gcs" {
    bucket = "interstellar-route-planner-tfstate"
    prefix = "terraform/state"
  }
}
