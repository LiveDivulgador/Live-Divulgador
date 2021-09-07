
let orderapp = new Vue({

    el: "#liveapp",
    delimiters: ['[[', ']]'],
    data(){
        return{
            twitch_name: "",
            twitch_id: "",
            twitter: "",
            allow_print: "",
            category: "",
            hashtags: "",
            is_valid: false,
            command: "INSERT INTO livecoders (Nome,Id,Twitch,Twitter,OnStream,Print,Tipo,Hashtags) VALUES "
        }
    },
    methods:{
        get_twitch_id(){
            fetch("/get_streamer_id/?twitch_name="+ this.twitch_name, {
                method: "GET"
            
            }).then((resp) => {
                
                // Se o status code for 200
                if(resp.ok){
                    // Recebe a resposta com status code
                    return resp.json()    
                }
                else{
                    let err = new Error("Status code: " + resp.status)
                    err.resp = resp
                    err.status = resp.status
                    throw err;
                }
                
            
            }).then((result) => {
                
                // Caso encontre, guarda id
                this.twitch_id = result.id;

            }).catch(function(error){
                alert(error);
            });
        },

        validate(){
            this.is_valid = true;

            this.command += `('${this.twitch_name}',${this.twitch_id},'twitch.tv/${this.twitch_name}',\
                              '${this.twitter}',FALSE,${this.allow_print},'${this.category}',\
                              '${this.hashtags}');`
        }
    }
});