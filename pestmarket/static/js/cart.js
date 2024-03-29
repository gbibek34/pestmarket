function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getToken('csrftoken');


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

$(document).ready(function () {

    $(".checkout").hide();

    $(".btn-checkout").click(function () {
        $(".checkout").show();
        $(".btn-checkout").hide();
    });

    $(".btn-cancel").click(function () {
        $(".checkout").hide();
        $(".btn-checkout").show();
    });

    
});