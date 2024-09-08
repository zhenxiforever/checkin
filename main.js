const glados = async () => {
  const cookie = process.env.GLADOS
  if (!cookie) return
  try {
    const headers = {
      'cookie': cookie,
      'referer': 'https://glados.rocks/console/checkin',
      'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    }
    const checkin = await fetch('https://glados.rocks/api/user/checkin', {
      method: 'POST',
      headers: { ...headers, 'content-type': 'application/json' },
      body: '{"token":"glados.one"}',
    }).then((r) => r.json())
    const status = await fetch('https://glados.rocks/api/user/status', {
      method: 'GET',
      headers,
    }).then((r) => r.json())
    
    const res = [
      'Checkin OK',
      `${checkin.message}`,
      `Left Days ${Number(status.data.leftDays)}`,
      `${checkin.message}`.replace('Checkin!', `Days ${Number(status.data.leftDays)}!`)
    ]
    console.log(res)
    return res
  } catch (error) {
    const res = [
      'Checkin Error',
      `${error}`,
      `<${process.env.GITHUB_SERVER_URL}/${process.env.GITHUB_REPOSITORY}>`,
    ]
    console.log(res)
    return res
  }
}

const notify = async (contents) => {
  const token = process.env.NOTIFY
  if (!token || !contents) return
  await fetch(`https://www.pushplus.plus/send`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({
      token,
      title: contents[0],
      content: contents.join('<br>'),
      template: 'markdown',
    }),
  })
}

const notify_ft = async (contents) => {
  const token = process.env.FT_SEND_KEY
  if (!token || !contents) return
  
  const baseUrl = `https://sctapi.ftqq.com/${token}.send`;
  const params = {
    text: contents[3],
    desp: contents.join('\n\n')
  };
  console.log(params)
  
  // 使用 URL 和 URLSearchParams 搭配处理
  const url = new URL(baseUrl);
  url.search = new URLSearchParams(params);
  await fetch(url.toString(), {
    method: 'GET'
  })
}

const main = async () => {
  //await notify(await glados())
  await notify_ft(await glados())
}

main()
