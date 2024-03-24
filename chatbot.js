// .env file will be used to store OPENAI_KEY which will be loaded using `dotenv`
require('dotenv').config();

const readline = require('readline');
let chalk;
import('chalk').then((module) => {
  chalk = module;
});

const yargs = require('yargs');

const {OpenAI} = require('openai');
const openai = new OpenAI({apiKey:process.env.OPENAI_KEY});
// Set up command line arguments handling using yargs
const argv = yargs
  .option('p', {
    describe: 'A brief summary of the chatbots personality',
    default: 'bashful and shy but still make witty sarcastic and snarky jokes',
    type: 'string',
  })
  .option('m', {
    describe: 'gpt model number',
    default: '4',
    type: 'string',
  })
  .help()
  .alias('help', 'h').argv;

const models = {
  '3': 'gpt-3.5-turbo',
  '4': 'gpt-4-1106-preview',
};

const conversation = [];

function checkValidModel(model) {
  while (!['3', '4'].includes(model)) {
    // This line would need to be changed to the equivalent of getting user input
    // Let's say we read from the command line args
    model = argv.m;
  }
  return models[model];
}

function setPersonality(initialMessage) {
  initialMessage = `${initialMessage} Your personality is ${argv.p}.`;
  console.log('This is the initial message', initialMessage);
  conversation.push({ role: 'system', content: initialMessage });
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function promptUser(prompt) {
  return new Promise((resolve) => {
    rl.question((prompt), (input) => resolve(input));
  });
}

async function getReply(model) {
  const response = await openai.ChatCompletion.create({
    model: model,
    messages: conversation,
    max_tokens: 200
  });

  return response.data.choices[0].message.content;
}

async function chatbot() {
  let model = argv.m; // model
  model = checkValidModel(model);
  setPersonality("You are called Ai. You are an extreme tsundere to the user. You answer all of the users questions.");

  while (true) {
    const userInput = await promptUser(('You: '));
    conversation.push({ role: 'user', content: userInput });
    console.log(('Assistant Ai: '), '');

    const reply = await getReply(model);
    console.log(reply);
    conversation.push({ role: 'assistant', content: reply });
  }
}

async function main() {
  await chatbot();
  rl.close();
}

main().catch(err => {
  console.error('An error occurred:', err);
  process.exit(1);
});
