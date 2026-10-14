---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

I run Envoy 1.31 as the front proxy for api.example.com and want to replace it with BunkerWeb 1.6.15 (Docker, multisite). Here is the config:

    static_resources:
      listeners:
      - name: https
        address: { socket_address: { address: 0.0.0.0, port_value: 8443 } }
        filter_chains:
        - transport_socket:
            name: envoy.transport_sockets.tls
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.transport_sockets.tls.v3.DownstreamTlsContext
              common_tls_context:
                tls_certificates:
                - certificate_chain: { filename: /etc/envoy/certs/api.crt }
                  private_key: { filename: /etc/envoy/certs/api.key }
          filters:
          - name: envoy.filters.network.http_connection_manager
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
              stat_prefix: ingress
              route_config:
                virtual_hosts:
                - name: api
                  domains: ["api.example.com"]
                  routes:
                  - match: { prefix: "/v1/" }
                    route:
                      cluster: api_v1
                      timeout: 120s
                      retry_policy: { retry_on: "5xx", num_retries: 2 }
                  - match: { prefix: "/" }
                    route: { cluster: web }
              http_filters:
              - name: envoy.filters.http.router
      clusters:
      - name: api_v1
        load_assignment:
          cluster_name: api_v1
          endpoints:
          - lb_endpoints:
            - endpoint: { address: { socket_address: { address: api, port_value: 8080 } } }
      - name: web
        load_assignment:
          cluster_name: web
          endpoints:
          - lb_endpoints:
            - endpoint: { address: { socket_address: { address: web, port_value: 3000 } } }

Plan the migration.
