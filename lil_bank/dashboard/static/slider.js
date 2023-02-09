image1 = "https://i.pinimg.com/736x/11/dc/3d/11dc3d73e6b6cc8709fc22127d7d0aac.jpg"
image2 = "https://www.letsbegamechangers.com/wp-content/uploads/2019/02/mPAY24_sliderimg_cloud_LogoNEU_CH_V3.png"
image3 = "https://i.pinimg.com/564x/63/27/dc/6327dc05b7533e1896f37ed18d5926f8.jpg"
image4 = "https://i.pinimg.com/736x/4e/a3/6d/4ea36d38c859ffc0900b63371bd5fe12.jpg"

const images = [image1, image2, image3, image4];
  
  let currentImageIndex = 0;
  
  const sliderImage = document.getElementById("slider-image");

  sliderImage.src = images[currentImageIndex];
  setOnLoadImage = () => {
    sliderImage.src = images[currentImageIndex];
  }

  setInterval(() => {
    currentImageIndex = (currentImageIndex + 1) % images.length;
    sliderImage.src = images[currentImageIndex];
  }, 1000);