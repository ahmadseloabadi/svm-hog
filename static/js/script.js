$(document).ready(function () {
  // preview img
  $("#imageInput").on("change", function () {
    var file = this.files[0];
    if (file) {
      var reader = new FileReader();
      reader.onload = function (e) {
        $("#previewImg").attr("src", e.target.result);
        $("#preview").show();

        $("#previewImg-modal").attr("src", e.target.result);
      };
      reader.readAsDataURL(file); // Mengonversi gambar menjadi URL
    }
  });

  // predik tanpa refresh
  $("#uploadForm").on("submit", function (e) {
    e.preventDefault(); // Mencegah form dari refresh page

    var formData = new FormData();
    var fileInput = $("#imageInput")[0].files[0];

    if (!fileInput) {
      // Tampilkan modal error jika tidak ada file

      $("#loadingMessage").hide();
      $("#errorMessage").show();
      var statusModal = new bootstrap.Modal(
        document.getElementById("statusModal")
      );
      statusModal.show();
      return;
    }

    formData.append("file", fileInput);

    // Tampilkan modal loading
    $("#loadingMessage").show();
    $("#errorMessage").hide();
    var loadingModal = new bootstrap.Modal(
      document.getElementById("statusModal")
    );
    loadingModal.show();

    $.ajax({
      url: "/predict",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        // Menampilkan hasil prediksi
        loadingModal.hide(); // Sembunyikan modal loading setelah selesai
        $("#resultText").text(response.prediction);
        $("#noPredik").hide(); // Sembunyikan pesan h3
        $("#modalbodyimg").show(); // Tampilkan div modalbodyimg

        // Menampilkan gambar di result, prepro, dan gif
        displayImages(
          "resultSection",
          response.result_images,
          response.file_name,
          "result"
        );
        displayImages(
          "preproSection",
          response.prepro_images,
          response.file_name,
          "prepro"
        );
        displayImages(
          "gifSection",
          response.gif_images,
          response.file_name,
          "gif"
        );
      },
      error: function (response) {
        loadingModal.hide(); // Sembunyikan modal loading setelah selesai
        $("#loadingMessage").hide();
        $("#errorMessage").show();

        var statusModal = new bootstrap.Modal(
          document.getElementById("statusModal")
        );
        statusModal.show();
      },
    });
  });
  // Fungsi untuk menampilkan gambar
  function displayImages(sectionId, images, fileName, folder) {
    var section = $("#" + sectionId);
    section.empty(); // Kosongkan konten yang ada

    if (images.length > 0) {
      images.forEach(function (image) {
        var imgSrc =
          "/static/img/output/" + fileName + "/" + folder + "/" + image;
        if (section == "gifSection") {
          section.attr("src", imgSrc);
        } else {
          section.append('<img src="' + imgSrc + '" class="img-fluid" >');
        }
      });
    } else {
      section.append("<p>Tidak ada gambar di folder " + folder + "</p>");
    }
  }
  // Tombol Reset untuk menghapus semua data di form dan hasil prediksi
  $("#resetButton").on("click", function () {
    // Reset form input
    $("#uploadForm")[0].reset();
    $("#noPredik").show();
    $("#modalbodyimg").hide();
    $("#resultText").text("Belum dilakukan prediksi");

    $("#resultSection").empty();
    $("#preproSection").empty();
    $("#gifSection").empty();
    $("#previewImg").attr("src", "/static/img/assets/no-image.png");
    $("#gifSection").attr("src", "/static/img/assets/no-image.png");
  });
});
