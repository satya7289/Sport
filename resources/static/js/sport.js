var origin = window.location.origin;
if(!origin){
    origin = window.location.protocol + "//" + window.location.hostname + (window.location.port ? ':' + window.location.port: '');
}