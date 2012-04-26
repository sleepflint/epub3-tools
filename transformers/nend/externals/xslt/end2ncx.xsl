<?xml version="1.0"?>
<xsl:stylesheet version="1.0" 
                exclude-result-prefixes="epub x xsl"
                xmlns="http://www.daisy.org/z3986/2005/ncx/"
                xmlns:epub="http://www.idpf.org/2007/ops"
                xmlns:x="http://www.w3.org/1999/xhtml"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:template match="@*|node()">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="x:html">
    <ncx version="2005-1">
      <xsl:apply-templates/>
    </ncx>
  </xsl:template>
  <xsl:template match="x:head">
    <head>
      <meta name="dtb:uid" content="-1"/>
      <meta name="dtb:depth" content="-1"/>
      <meta name="dtb:totalPageCount" content="-1"/>
      <meta name="dtb:maxPageNumber" content="-1"/>
    </head>  
    <xsl:apply-templates/>
  </xsl:template>
  <xsl:template match="x:head/x:title">
    <docTitle>
      <text><xsl:value-of select="."/></text>
    </docTitle>  
  </xsl:template>

  <xsl:template match="x:nav[contains(@epub:type, 'toc')]">
    <navMap>
      <xsl:apply-templates/>
    </navMap>
  </xsl:template>
  <xsl:template match="x:nav[contains(@epub:type, 'toc')]//x:ol/x:li">
    <xsl:param name="points-before" select="1 + count(preceding::x:li[ancestor::x:nav[contains(@epub:type, 'toc')]])"/>
    <navPoint id="x{$points-before}" playOrder="{$points-before}">
      <xsl:apply-templates/>
    </navPoint>
  </xsl:template>

  <xsl:template match="x:nav[contains(@epub:type, 'toc')]//x:ol/x:li/x:a">
    <navLabel>
      <text><xsl:value-of select="."/></text>
    </navLabel>
    <content src="{@href}"/>
  </xsl:template>
</xsl:stylesheet>
