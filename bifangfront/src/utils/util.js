
const replaceRgx = /\{\{([\w]+)\}\}/g
function urlFormat(str,obj){
    if(!str || !obj) return str || ""
    
    return str.replace(replaceRgx,function($0,$1){
        return obj[$1]
    })
}

export {
    urlFormat
}