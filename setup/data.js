const mongoose = require('mongoose');
const fs = require('fs');

mongoose.connect('mongodb://localhost/pandaserve');

const Image = mongoose.model('Image', { filename: String });

console.log('Clearing historical images from MongoDB');
Image.remove({}).then(() => {
  const images = fs.readdirSync(`${__dirname}/../public/images`);

  console.log('Populating images in MongoDB');
  return Promise.all(images.map((image) => {
    const imageModel = new Image({ filename: image });
    imageModel.save();
  }))
})


