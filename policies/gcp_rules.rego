package terraform.gcp

deny contains msg if {
    resource := input.resource_changes[_]
    resource.type == "google_storage_bucket"
    resource.change.after != null
    not resource.change.after.uniform_bucket_level_access

    msg := sprintf(
        "security-risk: Bucket '%v' must have uniform bucket level access enabled.",
        [resource.name]
    )
}

deny contains msg if {
    resource := input.resource_changes[_]
    resource.change.after != null
    resource.change.after.region != "us-central1"

    msg := sprintf(
        "compliance: Resource '%v' must be in us-central1.",
        [resource.name]
    )
}
