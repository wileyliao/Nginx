## Build command:
```
docker run -d --name nginx_https_v --net ai -p 3000:3000 -v /C/Projects/Nginx/https/cert.key:/etc/nginx/ssl/cert.key:ro -v /C/Projects/Nginx/https/full_chain.crt:/etc/nginx/ssl/full_chain.crt:ro -v /C/Projects/Nginx/https/nginx.conf:/etc/nginx/conf.d/default.conf:ro nginx_https:volume
```

## Dockerfile:
```
FROM nginx:alpine

# 創建 SSL 證書目錄
RUN mkdir -p /etc/nginx/ssl && chmod 600 /etc/nginx/ssl

# 啟動 NGINX
CMD ["nginx", "-g", "daemon off;"]
```


## nginx.conf:
```
server {
    listen 3000 ssl;
    server_name www.kutech.tw;

    # SSL 設定
    ssl_certificate /etc/nginx/ssl/full_chain.crt;
    ssl_certificate_key /etc/nginx/ssl/cert.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Proxy headers 統一設置
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    # 路由設定
    location /gpu_status {
        proxy_pass http://gpu_status:3001/gpu_status;
    }

    location /gpu_status_fastapi {
        proxy_pass http://gpu_status_fastapi:3001/gpu_status;
    }

    location /po_vision {
        proxy_pass http://po_vision:3001/po_vision;
        client_max_body_size 20M;
        client_body_buffer_size 10M;
    }

    location /pill_rec_fast {
        proxy_pass http://pill_fastapi:3001/pill_recognition;
        client_max_body_size 20M;
        client_body_buffer_size 10M;
    }

    location /pill_rec_flask {
        proxy_pass http://pill_flask:3001/pill_recognition;
        client_max_body_size 20M;
        client_body_buffer_size 10M;
    }
}

```
