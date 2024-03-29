function readURL(input, destination) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            destination.innerText = "";
            let img = document.createElement("img");
            img.src = e.target.result;
            img.classList.add("img-default");
            img.style.height = "100%";
            destination.appendChild(img);
        }

        reader.readAsDataURL(input.files[0]); // convert to base64 string
    }
}

function readMultipleURL(input, destination) {
    if (input.files && input.files[0]) {

        destination.innerText = "";
        input.files.forEach(item => {
            var reader = new FileReader();

            reader.onload = function (e) {
                let column = document.createElement("div");
                column.classList.add("col-6");
                column.classList.add("col-sm-4");
                column.classList.add("col-md-4");
                column.classList.add("p-0");

                let img = document.createElement("img");
                img.src = e.target.result;
                img.classList.add("img-default", "img-thumbnail");
                img.style.height="100px"
                img.style.width = "100px";
                destination.appendChild(img);
                column.appendChild(img);
                destination.appendChild(column);
            }

            reader.readAsDataURL(item);
        });
        //reader.readAsDataURL(input.files[0]); // convert to base64 string
    }
}


$(document).ready(function () {
    let items = document.getElementsByClassName("image-form-section")
    for(item of items){
        item.querySelector("input").addEventListener("change", (e) => {
            readURL(e.target, item.querySelector(".img-display"))
        });
    }
    items = document.getElementsByClassName("form-extra-images")
    for(item of items){
        item.querySelector("input").addEventListener("change", (e) => {
            readMultipleURL(e.target, item.querySelector(".form-extra-images-container"))
        });
    }

});



(() => {

    function construct_url(key, value, exclude) {
        var url_list = window.location.href.split('?');
        var url = url_list[0] + '?'
        if (url_list.length > 1) {
            var queries = url_list[1];
            queries.split('&').forEach(function (i) {
                let left = i.split("=")[0]
                if (i.length !== 0 && left !== key && left !== exclude) {
                    url += i + '&'
                }
            });
        }
        url += key + '=' + value;
        window.location.replace(url);
        return False;
    }
})();