var count=0;
// For Adding Items
function AddItem(){
    let tableBody      =document.getElementById("final-table-body");
    var content ="";
    let del = '<td><button class="btn" onclick="DeleteItem(this)"><i class="fas fa-minus-circle"></i></button></td>';
   
    $(document).ready(function(){
        let sport   =$("#select-sport option:selected").text();
        let item    =$("#select-item option:selected").text();
        let brand   =$("#select-brand option:selected").text();
        let quality =$("#select-quality option:selected").text();
        let quantity=$("#select-quantity option:selected").text();
        // console.log(sport,item,brand,quality,quantity);
        content += AddData(sport,item,brand,quality,quantity);

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
        content += del;
        tableBody.innerHTML += content;
        console.log(count);
        count +=1;
        CleanData();
        CheckoutButton(); 
    }); 
}

// Utility function for adding <td> Data </td>
function AddData(sport,item,brand,quality,quantity){
    let ans = "<td>"+sport+"</td>";
    ans += "<td>"+item+"</td>";
    ans += "<td>"+brand+"</td>";
    ans += "<td>"+quality+"</td>";
    ans += "<td>"+quantity+"</td>";
    return ans;
}

// For Deleting items
function DeleteItem(e){
    let tableBody =document.getElementById("final-table-body").rows.length;
    if(tableBody>0){
         e.parentNode.parentNode.remove(e.parentNode);
    } 
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