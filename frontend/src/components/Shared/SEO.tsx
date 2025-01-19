import { Helmet } from 'react-helmet-async';

interface SEOProps {
  title: string;
  description: string;
  keywords?: string;
  image?: string;
  type?: string;
  author?: string;
}

const SEO = ({
  title,
  description,
  keywords,
  image,
  type = 'website',
  author = 'Устат',
}: SEOProps) => {
  const siteUrl = import.meta.env.VITE_APP_URL || 'https://ustat.kg';

  return (
    <Helmet>
      {/* Основные мета-теги */}
      <title>{title} | Устат</title>
      <meta name="description" content={description} />
      {keywords && <meta name="keywords" content={keywords} />}
      <meta name="author" content={author} />

      {/* Open Graph мета-теги */}
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:type" content={type} />
      <meta property="og:url" content={siteUrl} />
      {image && <meta property="og:image" content={image} />}
      <meta property="og:site_name" content="Устат" />

      {/* Twitter мета-теги */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      {image && <meta name="twitter:image" content={image} />}

      {/* Дополнительные мета-теги для образовательной платформы */}
      <meta name="robots" content="index, follow" />
      <meta name="language" content="Russian" />
      <meta name="revisit-after" content="7 days" />
      <meta name="distribution" content="global" />
      <meta name="rating" content="general" />
    </Helmet>
  );
};

export default SEO;
