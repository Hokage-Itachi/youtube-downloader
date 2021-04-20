function getResolution() {
    var xhttp = new XMLHttpRequest();
    let url = document.getElementById("video_url").value;
    if (!url) {
        return
    }
    let select_res = document.getElementById("resolution");
    select_res.options.length = 0;
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("message").innerHTML = "";
            resp_arr = JSON.parse(this.responseText);
            for (let i = 0; i < resp_arr.length; i++) {
                var option = document.createElement("option");
                option.text = resp_arr[i];
                option.value = resp_arr[i];
                select_res.add(option);
            }

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
    let playlist_url = document.getElementById("playlist_link").value;
    if (!playlist_url) {
        return
    }
    var xhttp = new XMLHttpRequest();

    let min_length_resolution_list = 10;
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            console.log("Here");
            document.getElementById("playlist_container_message").innerHTML = "";
            let playlist_videos = document.getElementById("playlist_video");

            resp_arr = JSON.parse(this.responseText);
            for (let i = 0; i < resp_arr.length; i++) {
                let title = resp_arr[i]["title"];
                let video_url = resp_arr[i]['url'];
                let res_list = resp_arr[i]["resolutions"];

                let list = document.createElement("li");

                setupListItem(list, video_url, res_list, title);
                // console.log(i, res_list[0]);
                if (res_list.length < min_length_resolution_list) {
                    min_length_resolution_list = res_list.length;
                }


                // list.appendChild(select_res);

                playlist_videos.appendChild(list);
            }
            // let select_res = document.createElement("select");
            // select_res.setAttribute("name", "resolution");
            let res_list = resp_arr[0]["resolutions"];
            let index = res_list.length - min_length_resolution_list;
            // console.log(res_list)
            // console.log(res_list.length, min_length_resolution_list, res_list[min_length_resolution_list - 1]);

            document.getElementById("general_resolution").value = res_list[index];
            document.getElementById("playlist_url").value = playlist_url;
            // for (let j = 0; j < min_length_resolution_list; j++) {
            //     let option = document.createElement("option");
            //     option.text = res_list[j];
            //     option.value = res_list[j];
            //
            //     select_res.add(option);
            // }


        } else if (this.status == 404) {
            document.getElementById("playlist_container_message").innerHTML = "Playlist không tồn tại hoặc không có video";
        } else {
            document.getElementById("playlist_container_message").innerHTML = "Đợi trong giây lát...";
        }
    };
    xhttp.open("POST", "/get_playlist_video", true);
    xhttp.send(playlist_url);


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

    let select_res = document.createElement("select");
    select_res.setAttribute("name", "resolution");

    for (let j = 0; j < res_list.length; j++) {
        let option = document.createElement("option");
        option.text = res_list[j];
        option.value = res_list[j];
        if (j === Math.floor(res_list.length / 2)) {
            option.setAttribute("selected", "True");
        }
        select_res.add(option);
    }

    let form = document.createElement("form");
    form.setAttribute("action", "/download");
    form.setAttribute("method", "POST");

    let video_url_input = document.createElement("input");
    video_url_input.setAttribute("type", "hidden");
    video_url_input.setAttribute("value", video_url);
    video_url_input.setAttribute("name", "link");

    let submit_btn = document.createElement("input");
    submit_btn.setAttribute("class", "download-button");
    submit_btn.setAttribute("type", "submit");
    submit_btn.setAttribute("value", "Tải xuống");

    form.appendChild(select_res);
    form.appendChild(video_url_input);
    form.appendChild(submit_btn);

    right_column.appendChild(form);

    list.appendChild(left_column);
    list.appendChild(right_column);

}