$("document").ready(function() {
    console.log("in photo_modal.js")
})


let _active = null
let _index = 0
let _length = 0
function handleModal(idx, length) {
    _length = length
    _index = ((idx % _length) + _length) % _length

    if (_active !== null){
        _active.attr("hidden", true)
    }

    _active = $("#modalPhoto" + _index)
    _active.removeAttr('hidden') 

    $("#modalLabel").text(_active.attr("title"))
}


function changePhoto(direction) {
    if (direction == "next"){
        handleModal(_index + 1, _length)
    }
    else {
        handleModal(_index - 1, _length)
    }
}