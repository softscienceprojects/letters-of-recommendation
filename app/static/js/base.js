BASE_URL = window.location.host + "/";
//if (window.location.href.indexOf('/posts') > -1) {

confirm_action = function() {
    
}

destroy = function() {
    let id = window.location.pathname.split('/')[2]
    ///posts/<int:post_id>/delete/
    //"posts/" + pathname[2] +posts/${id}/
    return fetch("delete/", {method: "POST"})
    .then(response=>response.json())
    .then(response=>window.location.replace(response.next))
    .catch(error=>console.error(error))
};

