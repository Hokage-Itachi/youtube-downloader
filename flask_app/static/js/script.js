function getResolution() {
    let xhttp = new XMLHttpRequest();
    let url = document.getElementById("video_url").value;
    if (!url) {
        return;
    }
    if (!validate_input(url, "watch")) {
        return;
    }
    let select_res = document.getElementById("resolution");
    select_res.options.length = 0;
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("message").innerHTML = "";
            let resp_arr = JSON.parse(this.responseText);
            // console.log(resp_arr);
            setupSelectItem(select_res, resp_arr);
        } else {
            document.getElementById("message").innerHTML = "Đợi trong giây lát...";
        }
    };
    xhttp.open("POST", "/possible_resolution", true);
    xhttp.send(url);
}

function openTab(tabID) {
    if (tabID === "single_download") {
        document.getElementById("single_download_container").hidden = false;
        document.getElementById("playlist_download_container").hidden = true;
        document.getElementById("channel_download_container").hidden = true;

        document.getElementById("single_download").className = "active";
        document.getElementById("playlist_download").className = "";
        document.getElementById("channel_download").className = "";
    } else if (tabID === "playlist_download") {
        document.getElementById("single_download_container").hidden = true;
        document.getElementById("playlist_download_container").hidden = false;
        document.getElementById("channel_download_container").hidden = true;

        document.getElementById("single_download").className = "";
        document.getElementById("playlist_download").className = "active";
        document.getElementById("channel_download").className = "";
    } else {
        document.getElementById("single_download_container").hidden = true;
        document.getElementById("playlist_download_container").hidden = true;
        document.getElementById("channel_download_container").hidden = false;

        document.getElementById("single_download").className = "";
        document.getElementById("playlist_download").className = "";
        document.getElementById("channel_download").className = "active";
    }
}

function getPlayListVideos() {
    let playlist_url = document.getElementById("playlist_url").value;
    if (!playlist_url) {
        return
    }
    if (!validate_input(playlist_url, "playlist")) {
        return
    }
    document.getElementById("playlist_videos").innerHTML = "";
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            // console.log("Here");
            document.getElementById("playlist_message").innerHTML = "";
            let resp_arr = JSON.parse(this.responseText);
            setupUlItem("playlist_videos", resp_arr);


            document.getElementById("form_playlist_url").value = setupVideosURL(resp_arr);


        } else if (this.status == 404) {
            document.getElementById("playlist_message").innerHTML = "Channel không tồn tại hoặc không có video";
        } else {
            document.getElementById("playlist_message").innerHTML = "Đợi trong giây lát...";
        }
    };
    xhttp.open("POST", "/get_playlist_videos", true);
    xhttp.send(playlist_url);


}

function getChannelVideo() {
    let channel_url = document.getElementById("channel_url").value;
    if (!channel_url) {
        alert("Hãy nhập channel link.");
        return;
    }
    let result = validate_input(channel_url, "channel");
    if (result === false) {
        alert("Link channel không đúng.")
        return;
    } else if (result !== true) {
        channel_url = result;
    }
    document.getElementById("channel_videos").innerHTML = "";
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            // console.log("Here");
            document.getElementById("channel_message").innerHTML = "";
            let resp_arr = JSON.parse(this.responseText);
            setupUlItem("channel_videos", resp_arr);

            document.getElementById("form_channel_url").value = setupVideosURL(resp_arr);


        } else if (this.status == 404) {

            document.getElementById("channel_message").innerHTML = "Channel không tồn tại hoặc không có video";
        } else {
            document.getElementById("channel_message").innerHTML = "Đợi trong giây lát...";

        }
    };
    xhttp.open("POST", "/get_channel_videos", true);
    xhttp.send(channel_url);
}

function setupListItem(list, video_url, res_list, title) {
    let left_column = document.createElement("div");
    left_column.setAttribute("class", "left-column");

    let a = document.createElement('a');
    a.setAttribute("href", video_url);
    if (title.length > 25) {
        a.setAttribute("title", title);
        title = title.slice(0, 25) + "..."
    }
    a.innerText = title;

    left_column.appendChild(a);

    let right_column = document.createElement("div");
    right_column.setAttribute("class", "right-column");

    let left_half_column = document.createElement("div");
    left_half_column.setAttribute("class", "right-column-half");

    let right_half_column = document.createElement("div");
    right_half_column.setAttribute("class", "right-column-half");

    let select_res = document.createElement("select");
    select_res.setAttribute("name", "resolution");

    setupSelectItem(select_res, res_list)

    let form = document.createElement("form");
    form.setAttribute("action", "/video_download");
    form.setAttribute("method", "POST");

    let video_url_input = document.createElement("input");
    video_url_input.setAttribute("type", "hidden");
    video_url_input.setAttribute("value", video_url);
    video_url_input.setAttribute("name", "video_url");

    let submit_btn = document.createElement("input");
    submit_btn.setAttribute("class", "download-button");
    submit_btn.setAttribute("type", "submit");
    submit_btn.setAttribute("value", "Tải xuống");
    submit_btn.style.marginTop = "0";

    left_half_column.appendChild(select_res);
    right_half_column.appendChild(video_url_input);
    right_half_column.appendChild(submit_btn);
    form.appendChild(left_half_column);
    form.appendChild(right_half_column);
    // form.appendChild(submit_btn);

    right_column.appendChild(form);

    list.appendChild(left_column);
    list.appendChild(right_column);


}

function setupSelectItem(select, res_list) {

    for (let j = 0; j < res_list.length; j++) {
        let option = document.createElement("option");
        option.text = res_list[j];
        option.value = res_list[j];
        if (j === 0) {
            option.selected = true;
        }
        select.add(option);
    }

}

function setupUlItem(ul_id, resp_arr) {
    let list_videos = document.getElementById(ul_id);
    for (let i = 0; i < resp_arr.length; i++) {
        let title = resp_arr[i]["title"];
        let video_url = resp_arr[i]['url'];
        let res_list = resp_arr[i]["resolutions"];

        let list = document.createElement("li");

        setupListItem(list, video_url, res_list, title);

        list_videos.appendChild(list);
    }


}

function setupVideosURL(response_data) {
    videos_url = [];
    for (let i = 0; i < response_data.length; i++) {
        videos_url.push(response_data[i]['url']);
    }

    return videos_url;
}

function getListResolution(input_id, ui_id) {
    let res_list = [];
    let ul = document.getElementById(ui_id);
    let select_list = ul.querySelectorAll("select");

    for (let i = 0; i < select_list.length; i++) {
        res_list.push(select_list[i].value);
    }

    document.getElementById(input_id).value = res_list;
}

function validate_input(string, type) {
    let arr = string.split("/");
    let protocol = arr[0];
    let domain = arr[2];
    let action = arr[3];
    let hostname = protocol + "//" + domain + "/";
    if (hostname !== "https://www.youtube.com/") {
        return false;
    }

    if (action.split("?")[0] === type) {
        return true;
    }

    if (action === "channel" || action === "c") {
        if (arr[5] === "videos") {
            return true;
        } else if (!arr[5]) {
            // alert("Here")
            return string + "/videos";
        }
        return false;
    }
}