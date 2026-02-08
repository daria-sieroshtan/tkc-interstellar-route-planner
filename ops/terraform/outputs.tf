output "vm_external_ip" {
  description = "External IP address of the VM"
  value       = google_compute_address.static_ip.address
}
