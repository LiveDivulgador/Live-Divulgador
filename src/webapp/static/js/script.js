
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
            command: "",
            instruction: "insert"
        }
    },
    mounted: function(){
        this.cleanup(this.instruction);
    },
    methods:{
        cleanup(instruction){
            this.twitch_name = "";
            this.twitch_id = "";
            this.twitter = "";
            this.allow_print = "";
            this.category = "";
            this.hashtags = "";
            
            if(instruction == "insert"){
                this.command = "INSERT INTO livecoders (Nome,Id,Twitch,Twitter,OnStream,Print,Tipo,Hashtags) VALUES ";
            }
            else if(instruction == "update"){
                this.command = "UPDATE livecoders SET ";
            }
        },

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
            this.is_valid = ~this.is_valid;

            if(this.is_valid){

                if(this.instruction == "insert"){
                    this.command += `('${this.twitch_name}',${this.twitch_id},'twitch.tv/${this.twitch_name}',\
                                    '${this.twitter}',FALSE,${this.allow_print},'${this.category}',\
                                    '${this.hashtags}');`
                }
                else if(this.instruction == "update"){
                    
                    if(this.twitter != ""){
                        this.command += `Twitter='${this.twitter}',`;
                    }
                    if(this.allow_print != ""){
                        this.command += `Print=${this.allow_print},`;
                    }
                    if(this.category != ""){
                        this.command += `Tipo='${this.category}',`;
                    }
                    if(this.hashtags != ""){
                        this.command += `Hashtags='${this.hashtags}',`;
                    }

                    if(this.command != "UPDATE livecoders SET "){
                        this.command = this.command.slice(0, -1);
                        this.command += ` WHERE Id=${this.twitch_id};`;
                    }
                    else{
                        alert("Não modificou nada!");
                        this.cleanup(this.instruction);
                        this.is_valid = false;
                    }
                }
            }
            else{
                this.cleanup(this.instruction);
            }
        },
        change_instruction(instruction){
            this.cleanup(instruction);
            this.instruction = instruction;
        }
    }
});