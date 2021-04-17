var updateBtn = document.getElementsByClassName('update-cart')


for(var i = 0; i < updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        updateUserOrder(productId, action)
    })
}

function updateUserOrder(productId, action){
    var url = '/products/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type': 'application',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}

$(".checkout").hide();

    $(".btn-checkout").click(function () {
        $(".checkout").show();
    });

    $(".btn-cancel").click(function () {
        $(".checkout").show();
    });