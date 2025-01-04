for service in auth gateway converter; do
    docker build -t codetyperpro/$service:latest ./$service && \
    docker push codetyperpro/$service:latest
done