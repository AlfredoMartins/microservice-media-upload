for dir in ./auth ./converter ./gateway ./rabbit; do
  kubectl delete -f $dir/manifests
  kubectl apply -f $dir/manifests
done