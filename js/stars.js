// Get the number of stars of a given GitHub repository
async function getStars(repo) {
    var url = "https://api.github.com/repos/psaegert/" + repo

    var response = await fetch(url, {
        method: "GET",
        headers: {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "psaegert.github.io"
            }
        })
    var data = await response.json()

    return data.stargazers_count;
}