import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    const { registration_mark } = req.body;

    const spawn = require('child_process').spawn;
    const process = spawn('python', ['./cartax.py', registration_mark]);

    let resultData = '';

    process.stdout.on('data', (data: any) => {
      resultData += data.toString('utf-8');
    });

    process.stderr.on('data', (data: any) => {
      console.error(`Error: ${data}`);
      res.status(500).json({ error: 'Internal Server Error' });
    });

    process.on('close', (code: any) => {
      if (code === 0) {
        try {
          const parsedResult = JSON.parse(resultData);
          res.status(200).json(parsedResult);
        } catch (error) {
          console.error('Error parsing JSON:', error);
          res.status(500).json({ error: 'Internal Server Error' });
        }
      } else {
        res.status(500).json({ error: 'Internal Server Error' });
      }
    });
  } else {
    res.status(405).json({ error: 'Method Not Allowed' });
  }
}
