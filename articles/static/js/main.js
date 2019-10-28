function shuffleList(listId)
{
    var ul = document.getElementById(listId)
    // if there are only 2 items in the list flip the order because with random ordering they would remain unchanged 50% of the time
    if (ul.children.length == 2) {
        ul.appendChild(ul.children[0]);
    }
    else {
        // otherwise reorder the list items randomly
        for (var i = ul.children.length; i >= 0; i--) {
            ul.appendChild(ul.children[Math.random() * i | 0]);
        }
    }
}

function addComment(articleUuid)
{
    var ul = document.getElementById("comment-list")
    var input = document.getElementById("comment-input")
    var comment = input.value.trim();
    if (comment === "")
        return;
    
    axios.post('/comments', {comment: comment, article_uuid: articleUuid})
        .then(function (response) {
            if (ul.children.length == 1 && ul.children[0].textContent == "No comments yet!") {
                ul.children[0].textContent = input.value;
            }
            else {
                var li = document.createElement("li");
                li.appendChild(document.createTextNode(input.value));
                ul.appendChild(li)
            }
            input.value = "";
        })
        .catch(function (error) {
            console.log(error);
        });
}
