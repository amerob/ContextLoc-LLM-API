import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
import re
def extract_geolocations(input_string):
        pattern = r'Answer:\s*([\s\S]+?)\s*(?:\n|$)'
        match = re.search(pattern, input_string)

        if match:
            geolocations= match.group(1).strip()
            return geolocations
class mlmodel:

    def __init__(self):#access_token,base_model_id,bnb_config,base_model,tokenizer,ft_model):
        self.access_token = "YOUR_ACCESS_TOKEN_FROM_HUGGING_FACE"
        self.base_model_id = "AIDC-ai-business/Marcoroni-7B-v3"
        self.bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )

        self.base_model = AutoModelForCausalLM.from_pretrained(
            self.base_model_id,  
            quantization_config=self.bnb_config,  
            device_map="auto",
            trust_remote_code=True,
            use_auth_token=True,

        )

        self.tokenizer = AutoTokenizer.from_pretrained(self.base_model_id, add_bos_token=True, trust_remote_code=True)
        
        self.ft_model = PeftModel.from_pretrained(self.base_model,"checkpoint-300/")
    
        
    def finalfunc(self,ini):
        eval_prompt = " ### The following sentence might contain a possible name of a geolocation. your task is to find the name/names of geolocation/geolocations. : "+ini+" \n ### Answer: "
        model_input = self.tokenizer(eval_prompt, return_tensors="pt").to("cuda")

        self.ft_model.eval()
        with torch.no_grad():
            returnVAL = (self.tokenizer.decode(self.ft_model.generate(**model_input, max_new_tokens=30, repetition_penalty=1.15)[0], skip_special_tokens=True))
            print(returnVAL)
            
            return extract_geolocations(returnVAL)


#def finalfunc(ini):
    #access_token = "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"
    #base_model_id = "AIDC-ai-business/Marcoroni-7B-v3"
    #bnb_config = BitsAndBytesConfig(
    #    load_in_4bit=True,
    #    bnb_4bit_use_double_quant=True,
    #    bnb_4bit_quant_type="nf4",
    #    bnb_4bit_compute_dtype=torch.bfloat16
    #)
#
    #base_model = AutoModelForCausalLM.from_pretrained(
    #    base_model_id,  
    #    quantization_config=bnb_config,  
    #    device_map="auto",
    #    trust_remote_code=True,
    #    use_auth_token=True,
    #    
    #)
#
    #tokenizer = AutoTokenizer.from_pretrained(base_model_id, add_bos_token=True, trust_remote_code=True)
#
#
#
#
#    from peft import PeftModel
#
#    ft_model = PeftModel.from_pretrained(base_model, "checkpoint-300/")
#
#
#
#    eval_prompt = " ### The following sentence might contain a possible name of a geolocation. your task is to find the name/names of geolocation/geolocations. "+ini+" \n ### Answer: "
#    model_input = tokenizer(eval_prompt, return_tensors="pt").to("cuda")
#
#    ft_model.eval()
#    with torch.no_grad():
#        return (tokenizer.decode(ft_model.generate(**model_input, max_new_tokens=30, repetition_penalty=1.15)[0], skip_special_tokens=True))