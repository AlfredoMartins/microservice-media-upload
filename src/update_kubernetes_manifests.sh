for dir in ./rabbit ./auth ./gateway ./converter ; do
  kubectl delete -f $dir/manifests
  kubectl apply -f $dir/manifests
done

for deploy in auth gateway converter; do
  kubectl scale deployment --replicas=1 $deploy
done