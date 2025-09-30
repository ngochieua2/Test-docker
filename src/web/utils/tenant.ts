export function extractTenantFromHost(host: string): string {
  if (!host) return "default";

  // For development
  if (host.includes("localhost")) {
    const subdomain = host.split(".")[0];
    return subdomain === "localhost" ? "default" : subdomain;
  }

  // For production
  const parts = host.split(".");
  if (parts.length >= 3) {
    return parts[0]; // subdomain
  }

  return "default";
}

export function getTenantConfig(tenant: string) {
  // Return tenant-specific configuration
  return {
    name: tenant,
    domain: `${tenant}.yourapp.com`,
    logo: `/tenants/${tenant}/logo.png`,
    theme: {
      primary: "#F8B738",
      secondary: "#F95085",
    },
  };
}
