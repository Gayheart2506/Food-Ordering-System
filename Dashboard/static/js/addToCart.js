// let count = 1;
// document.querySelector('.increase-sign').onclick = function(){
//     count++;
//     document.querySelector('#quantity').innerHTML = count;
// document.querySelector('.decrease-sign').onclick = function(){
//     if (count > 1){
//     count--;
//     document.querySelector('#quantity').innerHTML = count;
//     }else {
//     document.querySelector('#quantity').innerHTML = count;
//     }
//     }  
// };


// Add to cart functionality 
// $(document).ready(function () {
//     $('.increase-sign').click(function(e){
//         e.preventDefault();

//         var inc_value = $(this).closest('selection-container').find('#quantity').val();
//         if(inc_value < 10)
//         {
//             inc_value++;
//             $(this).closest('.selection-container').find('#quantity').val(inc_value);
//         }
//     });
// });

//Increasing and decreasing quantity 
$(document).ready(function() {
    let count = 1;
  
    $('.increase-sign').on('click', function() {
      count++;
      $('#quantity').html(count);
    });
  
    $('.decrease-sign').on('click', function() {
      if (count > 1) {
        count--;
      }
      $('#quantity').html(count);
    });

    // $('.cart-btn').click(function (e) { 
    //     e.preventDefault();
        
    //     var food_id = $('.food_id').val();
    //     var food_qty = $('#quantity').text();
    //     $.ajax({
    //         type: "POST",
    //         url: "{% url 'addtocart' %}",
    //         data: {
    //             'id': food_id,
    //             'qty': food_qty,
    //             csrfmiddlewaretoken: '{{csrf_token}}'
    //         },
    //         dataType: "json",
    //         success: function (response) {
    //             console.log(response)
                
    //         }
    //     });

    // });
});
  