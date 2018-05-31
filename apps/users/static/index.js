$(document).ready(function(){
    //Current page is one.
    $("#page-0").addClass("currentPage");
    
    //Listener for page changes.
    $("#page-navigator").on("click", "span", function(){
        $(".currentPage").removeClass("currentPage");
        let page = $(this).attr("data");
        $(`#page-${page}`).addClass("currentPage");
        book.changePage(page);
        updateCurrentDisplay(book);
    });
    
    //Create book to manage current display and populate with data.
    var book = new Book();
    $.get('/users/ajax-index', function(res){
        book.update(res.users)
    });

    //Submission of new user data.
    $("#create-user").submit(function(e){
        let that = this;
        e.preventDefault();

        $.post('/users/create', $(this).serialize(),function(res){
            if (res.errors.length > 0) {
                displayErrors(res)
            } else {
                $("#errors").attr("hidden",true);
                book.update(res.users)                
                updateCurrentDisplay(book);
                updatePageDisplay(book);
                $(that).trigger('reset');
            }
        });

    });
});


function displayErrors(res) {
    let errorMessage = "<ul>";
    for (error of res.errors) {
        errorMessage += `<li>${error}</li>`
    }
    erroMessage = "</ul>"
    $("#errors").attr("hidden", false);
    $("#errors").html(errorMessage);
}

function updatePageDisplay(book) {
    console.log("updating page display");
    let pageDisplay = "";
    for (i = 0; i < book.totalPages; i++) {
        if (i == book.currentPage) {
            pageDisplay += `<span data="${i}" id="page-${i}" class="currentPage"> ${i + 1} </span>`
        } else {
            pageDisplay += `<span data="${i}" id="page-${i}"> ${i + 1} </span>`
        }
    }
    $("#page-navigator").html(pageDisplay);
}

function updateCurrentDisplay(book) {
    let userDisplay = "";
    for (user of book.view) {
        created_at = new Date(Date.parse(user.created_at));
        created_at = created_at.toLocaleString();
    
        userDisplay += `
                            <tr>
                                <td>${user.first_name} ${user.last_name}</td>
                                <td>${user.email}</td>
                                <td>${created_at}</td>
                            </tr>
                        `
    }
    $("#user-display").html(userDisplay);
}

//Book with hard-coded page-length of 5, page display starts at 1 but page variable starts at 0 (N.B.!)
class Book {
    constructor() {
        this.data = null;
        this.total = null;
        this.currentPage = 0;
        this.totalPages = 0;
        this.view = null;
    }
    update(data){
        this.data = data;
        this.total = data.length;
        this.totalPages = Math.ceil(this.total / 5);
        this.changePage(this.currentPage)
    }
    changePage(pageNumber){
        this.currentPage = pageNumber;
        this.view = this.data.slice(pageNumber*5,pageNumber*5+5);
    }
}