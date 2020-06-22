BASE_URL = window.location.host + "/";
//if (window.location.href.indexOf('/posts') > -1) {

destroy = function() {
    let id = window.location.pathname.split('/')[2]
    ///posts/<int:post_id>/delete/
    //"posts/" + pathname[2] +posts/${id}/
    return fetch("delete/", {method: "POST"})
    .then(
        response=>response.json()
    ) //.then(data=>console.log(data))
    .then(response=>window.location.replace(response.next))
    //.catch((error) => console.error(error))
    //window.location.replace(BASE_URL)
    // destroy = (url, id) => {
    //     return fetch(url/id, 
    //     method: “DELETE”
    //     }).then(response=>response.json()}
};

