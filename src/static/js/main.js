const sendButton = document.getElementById("sendButton");
const chatBox = document.getElementById("chatBox");
const input = document.getElementById("textval");


function sendMessage(text,time)
{
    //FETCH JSON HERE
    const bodi = {
        "headers" : {
            "content-type" : "application/json"
        },
        "body": JSON.stringify({
            "message" : text
        }),
        "method" : "POST"
    }
    let hasilRequest
    //DOING POST REQUEST HERE
    fetch('/api/messaging', bodi)
        .then(data=>{return data.json()})
        .then(res=>{
            //console.log(res)
            hasilRequest = res
        })
        .then(()=>{
            //console.log(hasilRequest)
            let div1 = document.createElement('div');
            div1.classList.add("media","w-50","ml-auto","mb-3");
            let div2 = document.createElement('div');
            div2.classList.add("media-body");
            let div3 = document.createElement('div');
            div3.classList.add("bg-primary","rounded","py-2", "px-3", "mb-2");

            let pTime = document.createElement('p');
            pTime.classList.add("small","text-white");
            pTime.innerHTML = time;

            let pText = document.createElement('p');
            pText.width = 50;
            pText.classList.add("text-small","mb-0" ,"text-white");
            pText.innerHTML = text;

            div3.appendChild(pText);
            div2.appendChild(div3);
            div2.appendChild(pTime);
            div1.appendChild(div2);
            chatBox.appendChild(div1);

            //ISI PESAN DISINI CUY
            hsl = hasilRequest.header + "<br>"
            hasilRequest.pesan.forEach((i) => {
                hsl = hsl + i + "<br>"
            })

            botMessage(hsl,dateFormat());
            chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch(error=>console.log(error))

    input.value= "";
}

function botMessage(text,time)
{
    let div1 = document.createElement('div');
    div1.classList.add("media","w-50","mb-3");
    let div2 = document.createElement('div');
    div2.classList.add("media-body","ml-3");
    let div3 = document.createElement('div');
    div3.classList.add("bg-light","rounded","py-2", "px-3", "mb-2");

    let pTime = document.createElement('p');
    pTime.classList.add("small","text-white");
    pTime.innerHTML = time;

    let pText = document.createElement('p');
    pText.width = 50;
    pText.classList.add("text-small","mb-0" ,"text-muted");
    pText.innerHTML = text;

    let logo = document.createElement('img');
    logo.src = "../static/asset/200 (1).gif";
    logo.alt = "bot";
    logo.width = "50";
    logo.classList.add("rounded-circle")

    div3.appendChild(pText);
    div2.appendChild(div3);
    div2.appendChild(pTime);
    div1.appendChild(logo);
    div1.appendChild(div2);
    chatBox.appendChild(div1);
}

function dateFormat()
{
    let date = new Date();
    let month = date.getMonth();
    let hour = date.getHours();
    let minute = date.getMinutes();
    let datenum = date.getDate();
    let days = new Array(7);
    days[0] = "Sun";
    days[1] = "Mon";
    days[2] = "Tue";
    days[3] = "Wed";
    days[4] = "Thu";
    days[5] = "Fri";
    days[6] = "Sat";
    let day = days[date.getDay()]
    return day+", "+datenum+"/"+month+" "+hour+":"+minute
}

botMessage("Halo!, Selamat datang di REVOLT BOT!", dateFormat());
sendButton.onclick = ()=>sendMessage(input.value, dateFormat());