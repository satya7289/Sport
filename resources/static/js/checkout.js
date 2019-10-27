// for assigning each delete button to id , so it is easy to delete crossponding
var count=0;       

// For Adding Items
function AddItem(){
    let tableBody      =document.getElementById("final-table-body");
    var content ="";
    let del = '<td><button class="btn" onclick="DeleteItem(this)" id="'+ count +'"><i class="fas fa-minus-circle"></i></button></td>';
   
    $(document).ready(function(){
        let sport   =$("#select-sport option:selected").text();
        let item    =$("#select-item option:selected").text();
        let brand   =$("#select-brand option:selected").text();
        let quality =$("#select-quality option:selected").text();
        let quantity=$("#select-quantity option:selected").text();
        // console.log(sport,item,brand,quality,quantity);

        if(sport==""||item==""||brand==""||quality==""||quantity==""){
            message="";
            if(sport=="") message="Select sport's name";
            else if(item=="") message="Select equipment's name";
            else if(brand=="") message="Select brand of item";
            else if(quality=="") message="Select quality of item";
            else if(quantity=="") message="Select Quantity of item";
            alert(message);
            return;
        }


        content += AddData(sport,item,brand,quality,quantity);
        content += del;
        tableBody.innerHTML += content;
        console.log("count variable: "+count);
        CleanData();
        CheckoutButton();
        count +=1; 
    }); 
}

// Utility function for adding <td> Data </td> and adding Input data to form.
function AddData(sport,item,brand,quality,quantity){
    let ans = "<td>"+sport+"</td>";
    ans += "<td>"+item+"</td>";
    ans += "<td>"+brand+"</td>";
    ans += "<td>"+quality+"</td>";
    ans += "<td>"+quantity+"</td>";

    let formData='<div id="form-'+count+'">';
    formData    +='<input type="hidden" name="sport-'+count+'" value="'+sport+'"></input>';
    formData    +='<input type="hidden" name="item-'+count+'" value="'+item+'"></input>';
    formData    +='<input type="hidden" name="brand-'+count+'" value="'+brand+'"></input>';
    formData    +='<input type="hidden" name="quality-'+count+'" value="'+quality+'"></input>';
    formData    +='<input type="hidden" name="quantity-'+count+'" value="'+quantity+'"></input>';
    formData +='</div>';
    // let formData='<div id="form-'+count+'">';
    // formData    +='<input type="text" name="sport-'+count+'" value="'+sport+'"></input>';
    // formData    +='<input type="text" name="item-'+count+'" value="'+item+'"></input>';
    // formData    +='<input type="text" name="brand-'+count+'" value="'+brand+'"></input>';
    // formData    +='<input type="text" name="quality-'+count+'" value="'+quality+'"></input>';
    // formData    +='<input type="text" name="quantity-'+count+'" value="'+quantity+'"></input>';
    // formData +='</div>';
    console.log(formData);
    $("#form-data").append(formData);
    return ans;
}

// Utility function for checking Dublicate Data
function Dublicate(tableBody,sport,item,brand,quality){
return
}

// For Deleting items
function DeleteItem(e){
    $(document).ready(function(){
        e.parentNode.parentNode.remove(e.parentNode);
        let id =  $(e).attr("id")
        $('#form-'+id).remove();  
    });
    CheckoutButton(); 
 }

// For Enabling and Disabling checkout button
function CheckoutButton(){
    let tableBody=document.getElementById("final-table-body");
    let checkout   = document.getElementById("form-checkout");
    let rowSize  = tableBody.rows.length;
    if(rowSize>0){
        checkout.disabled = false;
    }
    else{
        checkout.disabled = true;
    }
}

// For Cleaning all Selectd Data
function CleanData(){
    $(document).ready(()=>{
        $('#select-sport').val(false);
        $('#select-item').val(false);
        $('#select-brand').val(false);
        $('#select-quality').val(false);
        $('#select-quantity').val(false);
    });
}


// For showing All Checkout to entry
// function ViewAll(){
//     alert("sdf");
//     $(document).ready(()=>{
//         $("#checkout-home").hide();
//         $("#all-checkout").fadeIn();
       
//     });
// }

// For showing student roll no. for entry
function ShowStudent(){
    $(document).ready(()=>{
        $("#checkout-home").hide();
        $("#student-roll-no").fadeIn();
       
    });
}

// For showing Checkout Detail to entry
function ShowCheckoutDetail(){
    $(document).ready(()=>{
       
    // Add Name on the checkout page
    let roll_no=$("#select-roll-no option:selected").text();
    if(roll_no!=""){
        $("#student-roll-no").hide();
        $("#student-checkout-detail").fadeIn();
        $("#checkout h4").html(roll_no);
        $("#form-student-roll-no").attr("value",roll_no);
    }
    else{
        alert("Select Student Roll no");
    }
   
    });
}

// Functionality of back button
function back(){
    $(document).ready(()=>{
        // alert("aa");
       if($("#student-roll-no").is(":hidden") && $("#checkout-home").is(":hidden") && !$("#student-checkout-detail").is(":hidden")){
           $("#student-checkout-detail").hide();
           $("#checkout-home").hide();
           $("#student-roll-no").fadeIn();
           console.log("in");
       }  
       else if($("#student-checkout-detail").is(":hidden") && $("#checkout-home").is(":hidden") && !$("#student-roll-no").is(":hidden")){
            $("#student-checkout-detail").hide();
            $("#student-roll-no").hide();
            $("#checkout-home").fadeIn();
            console.log("out");
       }

    });
}

// Refresh all data for checkout
function Refresh(){
    $(document).ready(()=>{
        count =0;
        $("#form-data").html("");
        $("#final-table-body").html("");
        console.log("cound:"+count);

    });
}
