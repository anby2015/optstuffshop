function calc_shipping(){
    from = "city--blagoveshhensk"
    to = $("#destination :selected").val();
    $.cookie("city", to,{ path: '/' });
    weight = ($("#weight").html());
    $.getJSON("http://emspost.ru/api/rest?callback=?&method=ems.calculate",
        {
            from: from,
            to: to,
            weight: weight
        },
        function(data) {
            $("#shipping_cost").html(data.rsp.price + ' руб.');
            $("#shipping_time").html(data.rsp.term.min + '-' + data.rsp.term.max +  ' дней');
            price = parseFloat(($("#price_top").html()));
            $("#shipping_fee").html(price*0.06+ ' руб.');
        }
     );
}
function show_destenation_list(){
    $.getJSON("http://emspost.ru/api/rest/?method=ems.get.locations&callback=?&type=russia&plain=true",
    function(data){
        var row = "";
        $.each(data.rsp.locations, function(i,city){
           $("#destination").append('<option value="' + city.value + '">' + city.name + '</option>');
        });
        //$("#destination").append(row);
        $("#destination").children().filter("[value='"+$.cookie("city")+"']").attr("selected", "selected");
        $("#destination").attr("disabled","");
    }
    );
}

function cart_show(){
    $.get("/ajax/", {
        action: "cart_show"
    },
    function(data) {
        $("#cart").html(data);
        $(".cart_item_del").click(function(){
            id = parseInt($(this).parent().parent().attr('id'));
            cart_del(id);
        });
        $(".cart_item_add").click(function(){
            id = parseInt($(this).parent().parent().attr('id'));
            cart_add(id);
        });

    }
    );
}
function cart_add_current(){
        id =parseInt($("#product_id").html());
        $.get("/ajax/", {
            action: "cart_add",
            product_id: id
        },
        function(data) {
            cart_show();
            if(data!=-1){
            }

        }
        )
}

function cart_add(id){
    $.get("/ajax/", {
        action: "cart_add",
        product_id: id
    },
    function(data) {
        cart_show();
    }
    );
}



function cart_del(id){
    $.get("/ajax/", {
        action: "cart_del",
        product_id: id
    },
    function(data) {
        cart_show();
    }
    );
}



$(document).ready(function() {
    //карусель изображений
    $('#product_images').jcarousel({
        scroll: 1,
        visible: 1
    });
    cart_show();
    show_destenation_list();

   //высчитываем стоимость достваки
    $("#destination").change(calc_shipping)
    $("#add_to_cart").click(cart_add_current);
    
    $("#payment_option").change(function(){
        if ($(this).val()=='2')
             $("#cod_warning").slideUp('slow');
        if ($(this).val()=='1')
            $("#cod_warning").slideDown('slow');

    });



});