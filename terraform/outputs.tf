output "redshift_host" {
  value = module.storage.redshift_cluster_dns_name
}

output "redshift_port" {
  value = module.storage.redshift_cluster_port
}
