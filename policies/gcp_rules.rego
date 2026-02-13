package terraform.gcp

# Rule: Deny if a GCP Storage Bucket is public
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "google_storage_bucket"
  # Check for public access prevention
  resource.change.after.uniform_bucket_level_access != true
  msg := sprintf("security-risk: Bucket '%v' must have uniform bucket level access enabled.", [resource.name])
}

# Rule: Enforce specific region
deny[msg] {
  resource := input.resource_changes[_]
  resource.change.after.region != "us-central1"
  msg := sprintf("compliance: Resource '%v' must be in us-central1.", [resource.name])
}
