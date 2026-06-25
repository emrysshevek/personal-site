let select_collection = async (idx) => {
  $("#select_err").hide()
  $(".collection-details").hide()
  $(".collection-details").eq(idx).show()
  console.log(idx)
  console.log($(".collection-details").eq(idx))
}