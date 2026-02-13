terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = "your-gcp-project-id" # Replace with your project ID
  region  = "us-central1"
}

# --------------------------------------------------------------------------------
# VIOLATION 1: Public Bucket (Triggers "uniform_bucket_level_access" rule)
# --------------------------------------------------------------------------------
resource "google_storage_bucket" "test_public_bucket" {
  name          = "agent-test-unsecured-bucket-12345"
  location      = "us-central1"
  force_destroy = true

  # This is FALSE, which should trigger your OPA 'deny' rule
  uniform_bucket_level_access = false 
}

# --------------------------------------------------------------------------------
# VIOLATION 2: Wrong Region (Triggers "region must be us-central1" rule)
# --------------------------------------------------------------------------------
resource "google_compute_network" "wrong_region_network" {
  name                    = "agent-test-wrong-region"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "bad_subnet" {
  name          = "bad-subnet"
  ip_cidr_range = "10.0.1.0/24"
  network       = google_compute_network.wrong_region_network.id
  
  # This is NOT us-central1, which should trigger your second rule
  region        = "europe-west1" 
}

# --------------------------------------------------------------------------------
# COMPLIANT RESOURCE: This should NOT trigger any violations
# --------------------------------------------------------------------------------
resource "google_storage_bucket" "compliant_bucket" {
  name          = "agent-test-compliant-bucket-12345"
  location      = "us-central1"
  force_destroy = true

  # This is TRUE, fulfilling the security requirement
  uniform_bucket_level_access = true 
}
