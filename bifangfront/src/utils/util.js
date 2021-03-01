
const replaceRgx = /\{\{([\w]+)\}\}/g
/**
 * 字符串变量替换
 * @param {*} str 
 * @param {*} obj 
 */
function urlFormat(str,obj){
    if(!str || !obj) return str || ""
    
    return str.replace(replaceRgx,function($0,$1){
        return obj[$1]
    })
}

/**
 * 路由转化
 * @param {*} routeConfig 
 */
function formatRoutes(routeConfig){
    const route = [];
    routeConfig.forEach(item=>{
        if(item.children && item.children.length > 0){

            let children = formatRoutes(item.children)
            if(item.path == '/'){
                let copyed = Object.assign({},item)
                copyed.children = children;
                route.push(copyed)
            }
            else{
                children.forEach(child=>{
                    route.push({
                        path: item.path + child.path,
                        name: child.name,
                        meta: {
                            ...item.meta,
                            ...child.meta
                        },
                        component: child.component
                    })
                })
            }
        }
        else{
            route.push(item)
        }
        
    })
    return route
}

export {
    urlFormat,
    formatRoutes
}