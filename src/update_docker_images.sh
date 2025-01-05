for service in auth gateway converter notification; do
    docker build -t codetyperpro/$service:latest ./$service && \
    docker push codetyperpro/$service:latest
done