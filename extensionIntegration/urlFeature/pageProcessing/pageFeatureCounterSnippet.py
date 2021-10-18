import string


allCount = []
featureCount = []
pageData = "heh"

#normalize
pageData = pageData.lower()
featureCount.append(pageData.count('</form>'))
featureCount.append(pageData.count('formmethod="post"'))
featureCount.append(pageData.count('formmethod="get"'))
featureCount.append(pageData.count('</script>'))
featureCount.append(pageData.count('.js'))
featureCount.append(pageData.count('</iframe>'))
featureCount.append(pageData.count('</applet>'))
featureCount.append(pageData.count('</frame>'))
featureCount.append(pageData.count('type="submit'))
featureCount.append(pageData.count('input email'))
featureCount.append(pageData.count('password'))
featureCount.append(pageData.count('</button>'))
allCount.append(featureCount)
featureCount = []