# Nginx
nginx on docker(include SSL)

## SSL
>- Dockerfile
```
FROM nginx:alpine

# 複製 NGINX 配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 複製 SSL 憑證文件
COPY cert.crt /etc/nginx/ssl/cert.crt
COPY cert.key /etc/nginx/ssl/cert.key
COPY ca_bundle.crt /etc/nginx/ssl/ca_bundle.crt

# 暴露 HTTPS 端口
EXPOSE 3003

# 啟動 NGINX
CMD ["nginx", "-g", "daemon off;"]
```

>- nginx.conf
```
server {
    listen 3003 ssl;
    server_name kutech.tw;

    ssl_certificate /etc/nginx/ssl/cert.crt;
    ssl_certificate_key /etc/nginx/ssl/cert.key;
    ssl_trusted_certificate /etc/nginx/ssl/ca_bundle.crt;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location /gpu_status {
        proxy_pass http://gpu_status_ssl:3001/gpu_status;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    ... ...
}
```

## NORMAL
>- Dockerfile
```
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
```

>- nginx.conf
```
server {
    listen 3000;

    location /gpu_status {
        proxy_pass http://gpu_status:3001/gpu_status;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
   
    location /po_vision {
        proxy_pass http://po_vision:3001/po_vision;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        client_max_body_size 20M;
        client_body_buffer_size 10M;
    }
    ... ...
}
```
