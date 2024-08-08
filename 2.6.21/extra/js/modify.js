$(document).ready(function () {
    var int = setInterval(fixCount, 100);
    var busuanziSiteOffset = parseInt(6427684);  // 6427684 是需要减去的初始数值，每个人的不一样，自测一下便知
    function fixCount() {
        if ($("#busuanzi_container_site_pv").css("display") != "none") {
            if (parseInt($("#busuanzi_value_site_pv").html()) >= busuanziSiteOffset) {
                clearInterval(int);
                $("#busuanzi_value_site_pv").html(parseInt($("#busuanzi_value_site_pv").html()) - busuanziSiteOffset);
            }
        }
    }
});