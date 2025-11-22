import { Card } from "@/components/ui/card";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import testimonial1 from "@assets/generated_images/professional_woman_testimonial_headshot.png";
import testimonial2 from "@assets/generated_images/professional_man_testimonial_headshot.png";

// TODO: remove mock functionality
const testimonials = [
  {
    quote: "Kintsu helped me land 3 interviews in my first week. The AI tailoring is incredibly precise and the coaching gave me confidence I didn't know I needed.",
    author: "Sarah Chen",
    role: "Senior Product Manager",
    company: "TechCorp",
    image: testimonial1
  },
  {
    quote: "After months of rejections, I tried Kintsu. Within two weeks, I had offers from companies I thought were out of reach. The resume tailoring made all the difference.",
    author: "Marcus Johnson",
    role: "Software Engineer",
    company: "InnovateLabs",
    image: testimonial2
  },
  {
    quote: "The transparency and honesty in Kintsu's approach is refreshing. No false promises, just real tools that actually work. Highly recommend for anyone serious about their career.",
    author: "Priya Sharma",
    role: "Data Scientist",
    company: "Analytics Inc",
    image: testimonial1
  }
];

export function Testimonials() {
  return (
    <section className="py-20 md:py-32 bg-background">
      <div className="container mx-auto px-4 md:px-6">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold font-serif mb-4">
            Loved by job seekers
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Real stories from professionals who transformed their careers
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <Card
              key={index}
              className="p-6 space-y-4 hover-elevate transition-all duration-200"
              data-testid={`testimonial-${index}`}
            >
              <p className="text-muted-foreground leading-relaxed italic">
                "{testimonial.quote}"
              </p>
              <div className="flex items-center gap-3 pt-4 border-t">
                <Avatar>
                  <AvatarImage src={testimonial.image} alt={testimonial.author} />
                  <AvatarFallback>{testimonial.author.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                </Avatar>
                <div>
                  <div className="font-semibold">{testimonial.author}</div>
                  <div className="text-sm text-muted-foreground">
                    {testimonial.role} at {testimonial.company}
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
