function flashControl(URL) {
  document.write('<object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" codebase="http://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=8,0,0,0" width="327" height="247" id="flu-player" align="middle">');
  document.write('<param name="movie" value="fluflashplayer.swf" />');
  document.write('<param name="quality" value="high" />');
  document.write('<param name="bgcolor" value="#000000" />');
  document.write('<param name="allowFullScreen" value="true" />');
  document.write('<param name="flashvars" value="fluURL='+URL+'"/>');
  document.write('<embed src="fluflashplayer.swf" quality="high" bgcolor="#000000" width="327" height="247" name="flu-player" align="middle" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer" flashvars="fluURL='+URL+'"/>');
  document.write('</object>');
}
