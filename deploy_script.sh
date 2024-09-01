#!/bin/bash
    echo "Applying Kubernetes manifests..."
    kubectl --kubeconfig=$KUBECONFIG apply -f ~/api_pass_app/deployment.yaml
    echo "Fetching Minikube IP and NodePort..."
    minikubeIp=$(minikube -p project-app ip)
    nodePort=$(kubectl --kubeconfig=$KUBECONFIG get svc passapp-service -o jsonpath='{.spec.ports[0].nodePort}')
    echo "Application is accessible at http://${minikubeIp}:${nodePort}/password/"
