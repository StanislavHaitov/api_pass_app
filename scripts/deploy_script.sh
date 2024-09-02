#!/bin/bash
    echo "Applying Kubernetes manifests..."
    kubectl rollout restart deployment passapp-deployment
    echo "Fetching Minikube IP and NodePort..."
    minikubeIp=$(minikube -p project-app ip)
    nodePort=$(kubectl --kubeconfig=$KUBECONFIG get svc passapp-service -o jsonpath='{.spec.ports[0].nodePort}')
    echo "Application is accessible at http://${minikubeIp}:${nodePort}/password/"
