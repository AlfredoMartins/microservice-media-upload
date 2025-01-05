for service in auth gateway converter; do
    docker build --no-cache -t codetyperpro/$service:latest ./$service && \
    docker push codetyperpro/$service:latest
done