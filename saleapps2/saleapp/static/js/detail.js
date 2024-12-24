function addComment(productId){
    fetch(`/api/products/${productId}/comments`, {
        method: 'post',
        body: JSON.stringify({
            'content': document.getElementById('content').value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res=>res.json()).then(data=>{
        console.log(data);
    })
}