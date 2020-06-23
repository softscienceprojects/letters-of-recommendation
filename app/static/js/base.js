BASE_URL = window.location.host + "/";

window.app = {
    destroy: function() {
        return fetch("delete/", {method: "POST"})
        .then(response=>response.json())
        .then(response=>window.location.replace(response.next))
        .catch(error=>console.error(error))
    }

}